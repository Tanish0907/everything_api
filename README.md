# everything_api

<table>
    <tr>
        <th>PATH</th>   
        <th>CATAGORY</th>
        <th>METHODS</th>
    </tr>
    <tr><td>/youtube</td><td>YT</td><td>SEARCH</td></tr>
    <tr><td>/anime</td><td>ANIME</td><td>SEARCH,GET_ANIME_DATA</td></tr>
    <tr><td>/books/manga</td><td>MANGA</td><td>SEARCH,GET_MANGA_DATA</td></tr>
    <tr><td>/books/comics</td><td>COMICS</td><td>SEARCH,GET_COMIC_DATA</td></tr>
</table>
<h1>How to deploy</h1>
<h4>Build Image<h4>
<b>sudo docker build img_name .</b>
<h4>Docker</h4>
<b>sudo docker run -d --name=everything-api -p8000:8000 -v path to config:/app/CONFIG tanish0907/everything-api:2.0.2</b>
<h4>now go to ur config folder and create a jackett.json file if u want to use torrsearch function and put the foll in file</h4>
<b>{"url":"http:// ur ip:9117","api_key":"jackett api key"}</b>
<h4>jackett must be setup beforehand</h4>
# contributors 
mukund1606<a href="https://github.com/mukund1606/consumet.py">->Consumet.py</a>
