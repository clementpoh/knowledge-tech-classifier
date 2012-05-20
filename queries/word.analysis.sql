create table word_analysis as
select books.category as category
    , book_words.word as word
    , book_words.freq as freq
    , books.total as total
    , books.dist as dist from books
    , book_words
where books.file = book_words.file;
