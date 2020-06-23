import React, { Component } from 'react';
import PropTypes from 'prop-types';

class Summary extends Component {
    constructor() {
	super()

	this.state = {
	    data : null,
	    loading: true
	};
    }
    async componentDidMount() {
         if(this.props.phenotype1 != null){

	          const dataRequest = await fetch(`/colocation/${this.props.phenotype1}/summary?min_clpa=0.1`);
              const data = await dataRequest.json();

              if (data) { this.setState({  data: data, loading: false, }); }
         }
    }

    render() {
    if(this.props.phenotype1 == null){
        return <p></p>
    } else if(this.state.loading){
	    return <div>Loading ... </div>
	} else {
	    let summary = this.state.data;
	    return (<p>This region has {` ${ summary.count }`} colocations ,
		         unique genes {` ${ summary.unique_phenotype2 }`} ,
		         unique tissues {` ${ summary.unique_tissue2 }`}
		    </p>)
	}
    }
}

Summary.propTypes = {
    phenotype1: PropTypes.string
}

export default Summary;