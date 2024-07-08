# everything_api

<table>
    <tr>
        <th>PATH</th>   
        <th>CATAGORY</th>
        <th>METHODS</th>
    </tr>
    <tr><td>/manga</td><td>MANGA</td><td>SEARCH,GET_MANGA_DATA</td></tr>
    <tr><td>/comics</td><td>COMICS</td><td>SEARCH,GET_COMIC_DATA</td></tr>
    <tr><td>/torr/search</td><td>Torrent</td><td>SEARCH</td></tr>
</table>
<h1>How to deploy</h1>
<h4>Build Image<h4>
<b>sudo docker build img_name .</b>
<h4>Docker</h4>
<b>sudo docker run -d --name=everything-api -p8000:8000  tanish0907/everything-api:2.0.8</b>
also to access web ui go to frontend_web folder and run :
<b>npm run dev</b>


