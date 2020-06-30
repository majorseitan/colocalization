import React, { Component } from 'react';
import 'react-table/react-table.css';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import ColocalizationList from './components/colocalization'
import { SummaryCard } from './components/summary'
import Search from './components/search'
import SearchContextProvider from './contexts/SearchContext'

class App extends Component {
render() {
    return (
    <div>
	 <header></header>
	  <div id="content" className="content">
	     <SearchContextProvider>
	        <Search/>
	        <SummaryCard />
	        <p></p>
	        <ColocalizationList />
         </SearchContextProvider>
       </div>
    </div>
    );
  }
}

export default App;
