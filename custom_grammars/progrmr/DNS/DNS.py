import io
import dns.zone


def validate_dns(
    zone_text: str,
    origin: str = "example.com.",
) -> bool:
    """
    Validates that `zone_text` is syntactically a DNS zone file.

    Similar spirit to validate_json(): returns True/False only (no exceptions).
    """
    try:
        f = io.StringIO(zone_text)
        dns.zone.from_file(
            f,
            origin=origin,
            relativize=False,
            check_origin=False,  # fuzzing-friendly
        )
        return True
    except Exception:
        return False