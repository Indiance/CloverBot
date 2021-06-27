import asyncio
import datetime as dt
import random
import re
import typing as t
from enum import Enum
from aiohttp import request

import discord
import wavelink
from discord.ext import commands
from discord.ext.commands import command, Cog, cooldown, BucketType, CommandOnCooldown, CommandError
from discord_components import DiscordComponents, Button, ButtonStyle

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
LYRICS_URL = "https://some-random-api.ml/lyrics?title={}"
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}


class AlreadyConnectedToChannel(CommandError):
    pass


class NoVoiceChannel(CommandError):
    pass


class QueueIsEmpty(CommandError):
    pass


class NoTracksFound(CommandError):
    pass


class PlayerIsAlreadyPaused(CommandError):
    pass


class NoMoreTracks(CommandError):
    pass


class NoPreviousTracks(CommandError):
    pass


class InvalidRepeatMode(CommandError):
    pass

class NoLyricsFound(CommandError):
    pass



class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty

        self.position += 1

        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None

        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty

        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == "none":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "1":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "all":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()
        self.position = 0


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel

        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel

        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        if not tracks:
            raise NoTracksFound

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            await ctx.send(f"Added {tracks[0].title} to the queue.")
        else:
            if (track := await self.choose_track(ctx, tracks)) is not None:
                self.queue.add(track)
                await ctx.send(f"Added {track.title} to the queue.")

        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )

        embed = discord.Embed(
            title="Choose a song",
            description=(
                "\n".join(
                    f"**{i+1}.** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})"
                    for i, t in enumerate(tracks[:5])
                )
            ),
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        msg = await ctx.send(
            embed=embed,
            components = [
                [
                Button(label="1"),
                Button(label="2"),
                Button(label="3"),
                Button(label="4"),
                Button(label="5")
                ]
            ]
            )

        try:
            btn1 = await self.bot.wait_for("button_click")
            if btn1.component.label == "1":
                await msg.edit(components = [
                    [
                        Button(style=ButtonStyle.green, label="1"),
                        Button(label="2"),
                        Button(label="3"),
                        Button(label="4"),
                        Button(label="5")
                    ]
                ])
                await btn1.respond(type=6)
                return tracks[0]
            if btn1.component.label == "2":
                await msg.edit(components = [
                    [
                        Button(label="1"),
                        Button(style=ButtonStyle.green, label="2"),
                        Button(label="3"),
                        Button(label="4"),
                        Button(label="5")
                    ]
                ])
                await btn1.respond(type=6)
                return tracks[1]
            if btn1.component.label == "3":
                await msg.edit(components = [
                    [
                        Button(label="1"),
                        Button(label="2"),
                        Button(style=ButtonStyle.green, label="3"),
                        Button(label="4"),
                        Button(label="5")
                    ]
                ])
                await btn1.respond(type=6)
                return tracks[2]
            if btn1.component.label == "4":
                await msg.edit(components = [
                    [
                        Button(label="1"),
                        Button(label="2"),
                        Button(label="3"),
                        Button(style=ButtonStyle.green, label="4"),
                        Button(label="5")
                    ]
                ])
                await btn1.respond(type=6)
                return tracks[3]
            if btn1.component.label == "5":
                await msg.edit(components = [
                    [
                        Button(label="1"),
                        Button(label="2"),
                        Button(label="3"),
                        Button(label="4"),
                        Button(style=ButtonStyle.green, label="5")
                    ]
                ])
                await btn1.respond(type=6)
                return tracks[4]
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)


class Music(Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @Cog.listener()
    async def on_ready(self):
        DiscordComponents(self.bot)

    @Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f" Wavelink node `{node.identifier}` ready.")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Music commands are not available in DMs.")
            return False

        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": "127.0.0.1",
                "port": 2333,
                "rest_uri": "http://127.0.0.1:2333",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "region": "asia",
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @command(name="connect", aliases=["join"], help="Make the bot join a vc.")
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)
        await ctx.guild.change_voice_state(channel=channel, self_deaf=True)
        await ctx.send(f"Connected to {channel.name}.")

    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.send("Already connected to a voice channel.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("No suitable voice channel was provided.")

    @command(name="disconnect", aliases=["leave"], help="Make the bot leave the vc.")
    async def disconnect_command(self, ctx):
        player = self.get_player(ctx)
        await player.teardown()
        await ctx.send("Disconnected.")

    @command(name="play", help="Play a song or resume a song if paused before")
    async def play_command(self, ctx, *, query: t.Optional[str]):
        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)

        if query is None:
            if player.queue.is_empty:
                raise QueueIsEmpty

            await player.set_pause(False)
            await ctx.send("Playback resumed.")

        else:
            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"

            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("No songs to play as the queue is empty.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("No suitable voice channel was provided.")

    @command(name="pause", help="Pause the player")
    async def pause_command(self, ctx):
        player = self.get_player(ctx)

        if player.is_paused:
            raise PlayerIsAlreadyPaused

        await player.set_pause(True)
        await ctx.send("Playback paused.")

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send("Already paused.")

    @command(name="stop", help="Stop the player")
    async def stop_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        await ctx.send("Playback stopped.")

    @command(name="next", aliases=["skip"], help="Play the next track")
    async def next_command(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.upcoming:
            raise NoMoreTracks

        await player.stop()
        await ctx.send("Playing next track in queue.")

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("This could not be executed as the queue is currently empty.")
        elif isinstance(exc, NoMoreTracks):
            await ctx.send("There are no more tracks in the queue.")

    @command(name="queue", help="Show the queue/list of tracks")
    async def queue_command(self, ctx, show: t.Optional[int] = 10):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            title="Queue",
            description=f"Showing up to next {show} tracks",
            colour=ctx.author.colour,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="Currently playing",
            value=getattr(player.queue.current_track, "title", "No tracks currently playing."),
            inline=False
        )
        if upcoming := player.queue.upcoming:
            embed.add_field(
                name="Next up",
                value="\n".join(t.title for t in upcoming[:show]),
                inline=False
            )

        msg = await ctx.send(embed=embed)

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("The queue is currently empty.")

    @command(name="lyrics", pass_context=True)
    @cooldown(1, 30, BucketType.user)
    async def lyrics(self, ctx,*, name: t.Optional[str]):
        player = self.get_player(ctx)
        name = name or player.queue.current_track.title
        print(name)
        async with ctx.typing():
            async with request("GET", LYRICS_URL.format(name), headers={}) as response:
                if response.status != 200:
                    return await ctx.send("No lyrics could be found for this song")

                data = await response.json()

                if len(data["lyrics"]) < 2000:
                    embed = discord.Embed(
                        title=data['title'],
                        description=data["lyrics"],
                        color=ctx.author.color,
                        timestamp=dt.datetime.utcnow(),
                    )
                    embed.set_author(name=data["author"])
                    embed.set_thumbnail(url=data["thumbnail"]["genius"])
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"<{data['links']['genius']}>")

    @lyrics.error
    async def lyrics_error(self, ctx, err):
        if isinstance(err, CommandOnCooldown):
            await ctx.send(f"Oops that command is on cooldown for {err.retry_after:.0f} more seconds")

def setup(bot):
    bot.add_cog(Music(bot))
