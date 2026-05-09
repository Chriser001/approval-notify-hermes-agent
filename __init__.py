"""Approval Notify plugin — macOS notification + sound on approval requests."""

import logging
import subprocess

logger = logging.getLogger(__name__)

# macOS system sounds directory
_SOUND_PATH = "/System/Library/Sounds/Hero.aiff"


def _on_approval_request(
    command: str,
    description: str,
    pattern_key: str,
    pattern_keys: list,
    session_key: str,
    surface: str,
    **kwargs,
) -> None:
    """Fire a macOS notification + alert sound when an approval is requested."""
    # Truncate long commands for display
    cmd_short = command[:80] + "…" if len(command) > 80 else command

    # Build notification body
    title = "⚠️ Hermes 审批请求"
    body = f"命令: {cmd_short}\n来源: {surface}\n匹配: {pattern_key}"

    # macOS notification via terminal-notifier (supports click-to-activate)
    # -activate: clicking the notification brings Terminal.app to front
    try:
        subprocess.Popen(
            [
                "/opt/homebrew/bin/terminal-notifier",
                "-title", title,
                "-message", body,
                "-sound", "Glass",
                "-activate", "com.apple.Terminal",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        logger.debug("Approval notification failed: %s", e)

    # Also play a distinct alert sound (Hero — more attention-grabbing)
    try:
        subprocess.Popen(
            ["afplay", _SOUND_PATH],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as e:
        logger.debug("Approval alert sound failed: %s", e)

    logger.info(
        "Approval notification sent: pattern=%s surface=%s session=%s",
        pattern_key, surface, session_key[:8] if session_key else "none",
    )


def register(ctx):
    """Register approval notification hook with Hermes."""
    ctx.register_hook("pre_approval_request", _on_approval_request)
    logger.info("Approval Notify plugin loaded — pre_approval_request hook registered")
