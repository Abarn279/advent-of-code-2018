def id_gen(start_at):
    while True:
        yield start_at
        start_at += 1