import React, { Component } from 'react';

import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { createStore } from 'redux';
import { search_parameters , connector }  from './reducers/query'
import ColocationList from './components/colocation'
import Summary from './components/summary'
import Search from './components/search'
import { Provider } from 'react-redux';

const store = createStore(search_parameters);



class App extends Component {
  render(){
  console.log(this);
  const phenotype1 = this.props.phenotype1;
  const update_phenotype1 = this.props.update_phenotype1;
  return (
  <Provider store={store}>
    <div>
	 <header></header>
	  <div id="content">
	     <Search update_phenotype1={ update_phenotype1 } />
	     <div className="card">
                <h5 className="card-header">colocation</h5>
	        <div className="card-body">
  	           <Summary phenotype1={ phenotype1 } />
	        </div>
	     </div>
	     <p></p>
	     <ColocationList phenotype1={ phenotype1 } />
       </div>
    </div>
  </Provider>);
  }
}

export default connector(App);
