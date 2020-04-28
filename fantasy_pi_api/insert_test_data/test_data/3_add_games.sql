insert into fantasy_pi_schema.games_types
    ( 
        game_type_id, 
        game_type
    )
values
    ( 
        1, 
        'Technology'
    ),
    (
        2, 
        'All'
    );

insert into fantasy_pi_schema.games
    (
        game_id, 
        game_name, 
        game_fee, 
        game_date_id, 
        game_start, 
        game_end, 
        game_type_id, 
        game_type,
        is_public
    )
values
    (
        0, 
        'FunnyNameGame0', 
        10, 
        1, 
        '2019-12-30 14:30:00', 
        '2020-01-03 20:30:00', 
        1, 
        'Technology',
        True
    ),
    (
        1, 
        'FunnyNameGame1', 
        100, 
        1, 
        '2019-12-30 14:30:00', 
        '2020-01-03 20:30:00', 
        2, 
        'All',
        True
    ),
    (
        2, 
        'FunnyNameGame2', 
        5.25, 
        2, 
        '2020-01-06 14:30:00', 
        '2020-01-10 20:30:00', 
        1, 
        'Technology',
        False
    ),
    (
        3, 
        'FunnyNameGame3', 
        80.325, 
        2, 
        '2020-01-06 14:30:00', 
        '2020-01-10 20:30:00', 
        2, 
        'All',
        True
    );
