CREATE TABLE if not exists actions(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    event_time real, 
    scope text,
    type text,
    module text, 
    func text, 
    args text,
    url text,
    path text
);
