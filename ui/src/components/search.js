import React, { Component } from 'react';

class Search extends Component {
    constructor() {
	super()

	this.state = {
	    phenotype1 : [],
	    loading: true
	};
    }
    async componentDidMount() {
 	      const dataRequest = await fetch('/phenotype1?min_clpa=0.1');
          const data = await dataRequest.json();

          if (data) { this.setState({  data: data, loading: false, }); }
    }

    render(){
    const update_phenotype1 = this.props.update_phenotype1;
  	if(this.state.loading){
	    return <div>Loading ... </div>
	} else {

        return (<div>
                <p></p>
                <form>
                    <div className="form-group row">
                        <select defaultValue={'DEFAULT'}  onChange={ (e) => update_phenotype1(e.target.value) }>
                            <option disabled value="DEFAULT">Please select Phenotype1</option>
                            { this.state.data.map(c => <option key={c} value={ c }>{c}</option>) }
                         </select>
                    </div>
                </form>
                <p></p>
                </div>);
      }
  }
}

export default Search;
