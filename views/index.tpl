% include('form.tpl')
  <h2>記事一覧</h2>
% for entry in articles:
    <li><img src={{entry['user_image']}} width="50" height="50">
    <a href="{{ entry['url'] }}"> {{ entry['title'] }} </a> : <a href="https://qiita.com/{{ entry['user_id'] }}"> {{ entry['user_id'] }} </a>
% end
