from external_apis import mk2, ugc, gaumont


def book_with_provider(provider, theater_name, movie_name, date):
    if provider == "mk2":
        return mk2.book_seat(theater_name, movie_name, date)

    elif provider == "ugc":
        return ugc.reserve(movie_name, date)

    elif provider == "gaumont":
        return gaumont.book(movie_name=movie_name, session=date)

    else:
        raise ValueError("Unknown provider")