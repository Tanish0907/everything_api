import "./App.css";
import { Button, Pagination } from "react-bootstrap";
import { createRoot } from "react-dom/client";
import "mdb-react-ui-kit/dist/css/mdb.min.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import Header from "./components/header";
import { Manga_card } from "./components/Manga_cards";
import { Comic_card } from "./components/Comic_cards";
import { Torr } from "./components/torrent";
import { useState} from "react";
import { Route, Routes ,useLocation} from "react-router-dom";
import React from 'react';

function App() {
  const [card_list, setCard_list] = useState([]);
  const curr_pg=useLocation();
  let res = [];
  const create_cards = () => {
    setCard_list([]);
   
    if(curr_pg.pathname == "/"){
      
      for (let i = 0; i < res.length; i++) {
        card_list.push(
          <Manga_card id={res[i].id} name={res[i].title} img={res[i].cover} len={res[i].number_of_chapters} />,
        );
      }
      const root = createRoot(document.getElementById("manga_card_div"));
      root.render();
      root.render(card_list, document.getElementById("manga_card_div"));
    }
    else if(curr_pg.pathname=="/comics"){
     
      for (let i = 0; i < res.length; i++) {
        card_list.push(
          <Comic_card id={res[i].id} name={res[i].id} img={res[i].poster} stat={res[i].status} />,
        );
      }
      const root = createRoot(document.getElementById("comic_card_div"));
      root.render();
      root.render(card_list, document.getElementById("comic_card_div"));
    }
    else if(curr_pg.pathname=="/torrent"){
      
     
      for(let i=0;i<res.length;i++){
        card_list.push(<Torr link={res[i].link} mag={res[i].magnet} size={res[i].size} title={res[i].Title} cat={res[i].catagory} source={res[i].source}/>);
      }
      const root=createRoot(document.getElementById("torr_card_div"));
      root.render();
      root.render(card_list)
    }

  };
 
  


  function handle_SearchData(data) {
    res = data.data;
    res=Object.values(res);
    console.log(res)
    create_cards();  
  }

  return (
    <>
      <Header sendSearchData={handle_SearchData} />
      <Routes>
        <Route path="/" element={<div id="manga_card_div" className="manga"></div>} />
        <Route path="/comics" element={<div id="comic_card_div" className="comic"></div>} />
        <Route path="/torrent" element={<div id="torr_card_div" className="torr"></div>}/>
      </Routes>
    </>
  );
}

export default App;
