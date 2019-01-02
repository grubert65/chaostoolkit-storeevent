CREATE TABLE if not exists actions(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    event_time real, 
    type text,
    module text, 
    func text, 
    args text,
    url text,
    path text
);
