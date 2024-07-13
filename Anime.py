import click
import os
import sys
import tempfile
import subprocess
import urllib.parse
import requests
import json
import re
import shutil
from pathlib import Path

version_number = "4.8.10"

def external_menu(prompt):
    return subprocess.run(["rofi", "-sort", "-dmenu", "-i", "-width", "1500", "-p", prompt], capture_output=True, text=True).stdout

def launcher(use_external_menu, prompt, multi_flag=""):
    if use_external_menu == "0":
        result = subprocess.run(["fzf", "+m" if multi_flag == "" else multi_flag, "--reverse", "--cycle", "--prompt", prompt], capture_output=True, text=True)
        return result.stdout
    elif use_external_menu == "1":
        return external_menu(prompt)
    return None

def nth(prompt, multi_flag=""):
    stdin = sys.stdin.read()
    if not stdin:
        return 1
    lines = stdin.splitlines()
    if len(lines) == 1:
        print("\t".join(lines[0].split()[1:3]))
        return 0

    line = launcher("0", prompt, multi_flag)
    line = line.split()[0] if line else ""
    if line:
        print("\t".join([line.split()[1], line.split()[2]]))
        return 0
    return 1

def die(message):
    print(f"\033[1;31m{message}\033[0m", file=sys.stderr)
    sys.exit(1)

def dep_ch(deps):
    for dep in deps:
        if not shutil.which(dep):
            die(f"Program \"{dep}\" not found. Please install it.")

def get_links(url):
    episode_link = requests.get(url).text
    episode_link = episode_link.replace('},{', '\n')
    episode_link = re.findall(r'"link":"([^"]*)".*"resolutionStr":"([^"]*)".*', episode_link)
    if "vipanicdn" in episode_link or "anifastcdn" in episode_link:
        if "original.m3u" in episode_link:
            return episode_link
        else:
            extract_link = episode_link.split('>')[1]
            relative_link = re.sub(r'[^/]*$', '', extract_link)
            episode_link = requests.get(extract_link).text
            episode_link = re.sub(r'#,.*|,.*', 'p', episode_link).splitlines()
            episode_link = [f"{link}>{relative_link}{link}" for link in episode_link if link]
            episode_link.sort(reverse=True)
            return episode_link
    else:
        return episode_link

def provider_init(resp, regex):
    provider_id = re.search(regex, resp)
    provider_id = provider_id.group(1) if provider_id else ""
    provider_id = provider_id.replace("01", "9").replace("08", "0").replace("05", "=").replace("0a", "2")
    provider_id = provider_id.replace("0b", "3").replace("0c", "4").replace("07", "?").replace("00", "8")
    provider_id = provider_id.replace("5c", "d").replace("0f", "7").replace("5e", "f").replace("17", "/")
    provider_id = provider_id.replace("54", "l").replace("09", "1").replace("48", "p").replace("4f", "w")
    provider_id = provider_id.replace("0e", "6").replace("5b", "c").replace("5d", "e").replace("0d", "5")
    provider_id = provider_id.replace("53", "k").replace("1e", "&").replace("5a", "b").replace("59", "a")
    provider_id = provider_id.replace("4a", "r").replace("4c", "t").replace("4e", "v").replace("57", "o")
    provider_id = provider_id.replace("51", "i")
    provider_id = provider_id.replace("/clock", "/clock.json")
    return provider_id

def generate_link(provider, resp):
    if provider == 1:
        return provider_init(resp, "Sak :")
    elif provider == 2:
        return provider_init(resp, "Kir :")
    elif provider == 3:
        return provider_init(resp, "S-mp4 :")
    else:
        return provider_init(resp, "Luf-mp4 :")

def select_quality(links, quality):
    if quality == "best":
        return links[0].split('>')[1]
    elif quality == "worst":
        return links[-1].split('>')[1]
    else:
        for link in links:
            if quality in link:
                return link.split('>')[1]
        print("Specified quality not found, defaulting to best", file=sys.stderr)
        return links[0].split('>')[1]

def get_episode_url(id, mode, ep_no, quality):
    anime_api = f"https://api.allanime.day/api"
    episode_embed_gql = {
        "query": "query ($showId: String!, $translationType: VaildTranslationTypeEnumType!, $episodeString: String!) { episode( showId: $showId translationType: $translationType episodeString: $episodeString ) { episodeString sourceUrls } }",
        "variables": {
            "showId": id,
            "translationType": mode,
            "episodeString": ep_no
        }
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
    }
    resp = requests.post(anime_api, headers=headers, data=json.dumps(episode_embed_gql)).text
    resp = re.findall(r'"sourceUrl":"--([^"]*)".*"sourceName":"([^"]*)".*', resp)
    links = []
    for provider in [1, 2, 3, 4]:
        links.extend(generate_link(provider, resp))
    return select_quality(links, quality)

def search_anime(query):
    anime_api = f"https://api.allanime.day/api"
    search_gql = {
        "query": "query( $search: SearchInput $limit: Int $page: Int $translationType: VaildTranslationTypeEnumType $countryOrigin: VaildCountryOriginEnumType ) { shows( search: $search limit: $limit page: $page translationType: $translationType countryOrigin: $countryOrigin ) { edges { node { id title } } } }",
        "variables": {
            "search": {
                "query": query,
                "limit": 10,
                "page": 1,
                "translationType": "sub",
                "countryOrigin": "JP"
            }
        }
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
    }
    resp = requests.post(anime_api, headers=headers, data=json.dumps(search_gql)).text
    return resp

def syncplay_open(file_path, title):
    sp_conf = os.path.join(os.path.expanduser('~'), ".syncplay", "default.conf")
    if not os.path.exists(sp_conf):
        print("Syncplay configuration not found! Please set it up first", file=sys.stderr)
        sys.exit(1)
    with open(sp_conf) as f:
        sp_conf = f.read()
    sp_conf = re.sub(r'\\', r'\\\\', sp_conf)
    sp_conf = re.sub(r'\[Window]\s*Geometry=.*', r'[Window]\nGeometry=600x500+100+50', sp_conf)
    sp_conf = re.sub(r'(mediaFileOrStream)=(.*)', rf'\1={file_path}', sp_conf)
    sp_conf = re.sub(r'(streamPath|duration|position|fullscreen)=.*', '', sp_conf)
    with open(sp_conf, "w") as f:
        f.write(sp_conf)
    subprocess.run(["syncplay", "-f", sp_conf, "--force-gui", "--file", file_path, "--title", title])

def play_video(file_path, player, options, no_detach):
    if player == "mpv":
        cmd = ["mpv"]
        if no_detach:
            cmd.extend(options)
        else:
            cmd.extend(["--detach"] + options)
    else:
        cmd = [player] + options
    cmd.append(file_path)
    return subprocess.run(cmd).returncode

def download_video(url, dest):
    cmd = ["aria2c", url, "-d", dest]
    subprocess.run(cmd)

@click.command()
@click.option('-c', '--continue-watching', is_flag=True, help="Continue watching from history")
@click.option('-d', '--download', is_flag=True, help="Download the video instead of playing it")
@click.option('-D', '--delete-history', is_flag=True, help="Delete history")
@click.option('-s', '--syncplay', is_flag=True, help="Use Syncplay to watch with friends")
@click.option('-S', '--select-nth', is_flag=True, help="Select nth entry")
@click.option('-q', '--quality', default="best", help="Specify the video quality")
@click.option('-v', '--vlc', is_flag=True, help="Use VLC to play the video")
@click.option('-V', '--version', is_flag=True, help="Show the version of the script")
@click.option('-h', '--help', is_flag=True, help="Show this help message and exit")
@click.option('-e', '--episode', help="Specify the number of episodes to watch")
@click.option('--dub', is_flag=True, help="Play dubbed version")
@click.option('--rofi', is_flag=True, help="Use rofi instead of fzf for the interactive menu")
@click.option('--skip', is_flag=True, help="Use ani-skip to skip the intro of the episode (mpv only)")
@click.option('--no-detach', is_flag=True, help="Don't detach the player (useful for in-terminal playback, mpv only)")
@click.option('--exit-after-play', is_flag=True, help="Exit the player, and return the player exit code (useful for non-interactive scenarios, works only if --no-detach is used, mpv only)")
@click.option('--skip-title', help="Use given title as ani-skip query")
@click.option('-N', '--nextep-countdown', is_flag=True, help="Display a countdown to the next episode")
@click.option('-U', '--update', is_flag=True, help="Update the script")
@click.argument('query', required=False)
def main(continue_watching, download, delete_history, syncplay, select_nth, quality, vlc, version, help, episode, dub, rofi, skip, no_detach, exit_after_play, skip_title, nextep_countdown, update, query):
    if help:
        click.echo(main.get_help(click.Context(main)))
        return

    if version:
        click.echo(f"Version: {version_number}")
        return

    if update:
        click.echo("Updating the script...")
        update_script()
        return

    # Ensuring the necessary dependencies are installed
    dep_ch(["fzf", "rofi", "aria2c", "mpv", "vlc"])

    # Handling history if requested
    history_file = os.path.join(os.path.expanduser('~'), ".ani-cli.history")
    if delete_history:
        if os.path.exists(history_file):
            os.remove(history_file)
        click.echo("History deleted.")
        return

    if continue_watching:
        if not os.path.exists(history_file):
            die("No history found.")
        with open(history_file) as f:
            history = f.read().strip().split('\n')
        last_watched = history[-1]
        query, episode = last_watched.split('\t', 1)

    if not query:
        die("No query provided.")

    search_results = search_anime(query)
    anime_list = []
    print(search_results)
    '''for result in search_results['data']['shows']['edges']:
        anime_list.append(f"{result['node']['id']}\t{result['node']['title']}")'''
    if not anime_list:
        die("No anime found.")

    anime = anime_list[0]
    if len(anime_list) > 1 and not select_nth:
        anime = launcher("0", "Select Anime")
    if not anime:
        die("No anime selected.")

    anime_id, anime_title = anime.split('\t', 1)

    # Getting the episode URLs
    episode = episode or "1"
    episode_url = get_episode_url(anime_id, "sub" if not dub else "dub", episode, quality)

    # Downloading or playing the video
    if download:
        download_video(episode_url, ".")
    elif syncplay:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(requests.get(episode_url).content)
        syncplay_open(temp_file.name, anime_title)
    else:
        player = "vlc" if vlc else "mpv"
        options = []
        if skip:
            options.append("--no-resume-playback")
        if no_detach:
            options.append("--no-detach")
        if exit_after_play:
            options.append("--no-keep-open=yes")
        play_video(episode_url, player, options, no_detach)

    # Saving history
    with open(history_file, "a") as f:
        f.write(f"{query}\t{episode}\n")

if __name__ == "__main__":
    main()

