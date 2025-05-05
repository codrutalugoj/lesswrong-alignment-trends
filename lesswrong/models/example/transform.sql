with results as (
    select 
    post.title, 
    post.author_names, 
    post.tags as tags, 
    post.post_karma as karma
from trends 
LATERAL VIEW EXPLODE(posts) as post
WHERE NOT array_contains(post.tags, "Site Meta") 
)
select * into NewTable
from results;