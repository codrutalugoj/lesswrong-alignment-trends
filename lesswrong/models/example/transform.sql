WITH results AS (
  SELECT
    post.title as title,
    post.author_names as author_names,
    post.date as date,
    post.tags as tags,
    post.post_karma as karma
  FROM lesswrong_data as post
  WHERE NOT 'Site Meta' = post.tags
)
SELECT * INTO lesswrong_transformed FROM results