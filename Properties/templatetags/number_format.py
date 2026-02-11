from django import template

register = template.Library()

@register.filter
def abbreviate_number(value):
    """
    Abbreviate large numbers with K, M, B, T suffixes
    Example: 50000000 -> 50M, 1500000 -> 1.5M, 1200 -> 1.2K
    """
    try:
        value = float(value)
    except (ValueError, TypeError):
        return value

    if value >= 1_000_000_000_000:  # Trillion
        return f"{value / 1_000_000_000_000:.1f}T".rstrip('0').rstrip('.')
    elif value >= 1_000_000_000:  # Billion
        return f"{value / 1_000_000_000:.1f}B".rstrip('0').rstrip('.')
    elif value >= 1_000_000:  # Million
        return f"{value / 1_000_000:.1f}M".rstrip('0').rstrip('.')
    elif value >= 1_000:  # Thousand
        return f"{value / 1_000:.1f}K".rstrip('0').rstrip('.')
    else:
        return f"{value:.0f}"
