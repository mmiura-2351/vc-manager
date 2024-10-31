"""This module defines discord's event handler."""

from commands import voice_state_update_handler


def setup_event_handler(bot: any) -> None:
    """Voice channel event handler."""

    @bot.event
    async def _voice_state_update_handler(
        member: any,
        before: any,
        after: any,
    ) -> None:
        await voice_state_update_handler(member, before, after)
