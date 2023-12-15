def determine_gender(last_letter):
    if last_letter[-1].lower() in ['а', 'я']:
        return 'женский'
    else:
        return 'мужской'

def format_experience(diff):
    years = diff // 365
    months = (diff % 365) // 30
    days = (diff % 365) % 30
    return f'{f"{years} г. " if years != 0 else ""}{months} мес. {days} дн.'