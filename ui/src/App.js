import React, { Component } from 'react';

import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { createStore } from 'redux';
import { search_parameters , connector }  from './reducers/query'
import ColocalizationList from './components/colocalization'
import { SummaryCard } from './components/summary'
import Search from './components/search'
import { Provider } from 'react-redux';

const store = createStore(search_parameters);

class Content extends Component {
  render(){
  const phenotype1 = this.props.phenotype1;
  const update_phenotype1 = this.props.update_phenotype1;
  console.log(phenotype1);
  return (
    <div>
	 <header></header>
	  <div id="content" className="content">
	     <Search update_phenotype1={ update_phenotype1 } />
	     <SummaryCard phenotype1={ phenotype1 } />
	     <p></p>
	     <ColocalizationList phenotype1={ phenotype1 } />
       </div>
    </div>);
  }
}
const ConnectedContent = connector(Content);

class App extends Component {
render() {
    return (
      <Provider store={store}>
        <ConnectedContent />
      </Provider>
    );
  }
}

export default App;
