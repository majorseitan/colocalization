import axios from 'axios'
import React, { Component } from 'react';
import { SearchContext } from '../contexts/SearchContext';

class Search extends Component {
    constructor() {
	super()

	this.state = {
	    phenotype1 : [],
	    loading: true
	};
    }
    async componentDidMount() {
 	  const dataRequest = await fetch('/api/colocalization?min_clpa=0.1');
          const data = await dataRequest.json();

          if (data) { this.setState({  data: data, loading: false, }); }
    }

    static contextType = SearchContext;
    handleSubmit(e){
	const file = e.target.csv.files[0];
	var formData = new FormData();
	formData.append("csv", file);
	axios.post('/api/colocalization',
		   formData,
		   { headers: { 'Content-Type': 'multipart/form-data' } });
	// TODO update message with functional
	console.log('Form submited');
	e.preventDefault();
    }

    render(){
      const { updatePhenotype } = this.context;
  	if(this.state.loading){
	    return <div>Loading ... </div>
	} else {

        return (<div>
                <p></p>
                <form onSubmit={this.handleSubmit} className="form-inline" action="/api/colocalization" method="post" encType="multipart/form-data">
		<div className="form-group mb-2">
                        <select className="form-control" defaultValue={'DEFAULT'}  onChange={ (e) => updatePhenotype(e.target.value) }>
                            <option disabled value="DEFAULT">Please select Phenotype1</option>
                            { this.state.data.map(c => <option key={c} value={ c }>{c}</option>) }
                        </select>
		</div>
		<div className="form-group mb-2">
		<input className="form-control" type="file" name="csv" id="file"/>
		</div>
		<input className="form-control btn btn-primary mb-2" type ="submit" value="upload"/>
                </form>
                <p></p>
                </div>);
      }
  }
}

export default Search;
