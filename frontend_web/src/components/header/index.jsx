import { Navbar, Nav, NavbarBrand, Button } from "react-bootstrap";
import logo from "./logo.png";
//import search_logo from "./search.png";
import Form from "react-bootstrap/Form";
import "./index.css";
import axios from "axios";
import { useState } from "react";
import { Link,useLocation } from "react-router-dom";
function Header({ sendSearchData }) {
  const [message, setMessage] = useState("");
  const loc=useLocation();
  const get_url=(search_term)=>{
    switch (loc.pathname) {
      case '/':
        return `http://localhost:8000/manga/search?term=${search_term}`;

      case '/comics':
        return `http://localhost:8000/comic/search?term=${search_term}`;
      case '/torrent':
        return `http://localhost:8000/torr/search?term=${search_term}`
    }
  }
  const get_manga_search_data = async (search_term) => {
    const Url=get_url(search_term);
    console.log(Url);
    axios
      .get(Url)
      .then((res) => {
        //console.log(res);
        const data =res;
        //console.log(data.data);
        sendSearchData(data);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const handleChange = (event) => {
    setMessage(event.target.value);
  };
  const get_res = (event, params) => {
    console.log(params);
    event.preventDefault();
    get_manga_search_data(params);
  };

  return (
    <Navbar expand="lg" className="bg-body-tertiary navbar">
      <img src={logo} alt="Logo" className="logo" />
      <div className="pages">
        <Link to="/">Manga</Link>
        <Link to="/comics">Comics</Link>
        <Link to="/torrent">Torrent</Link>
      </div>
      <div className="searchandprofile">
        <Form.Control
          className="search_field"
          type="text"
          placeholder="search"
          value={message}
          onChange={handleChange}
        />
        <Button onClick={(event) => get_res(event, message)}>Search</Button>
        <div className="profile"></div>
      </div>
    </Navbar>
  );
}

export default Header;
