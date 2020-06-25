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

    async updateSummary(){
         if(this.props.phenotype1 != null){

	          const dataRequest = await fetch(`/api/colocalization/${this.props.phenotype1}/summary?min_clpa=0.1`);
              const data = await dataRequest.json();

              if (data) { this.setState({  data: data, loading: false, }); }
         }
    }

    async componentDidMount() { this.updateSummary(); }
    //async componentDidUpdate() { this.updateSummary(); }


    render() {
    if(this.props.phenotype1 == null){
        return <p></p>
    } else if(this.state.loading){
	    return <div>Loading ... </div>
	} else {
	    let summary = this.state.data;
	    return (<p>This region has {` ${ summary.count }`} colocalizations ,
		       {` ${ summary.unique_phenotype2 }`} unique genes  ,
		        {` ${ summary.unique_tissue2 }`} unique tissues
		    </p>)
	}
    }
};

Summary.propTypes = {
    phenotype1: PropTypes.string
};

class SummaryCard extends Component {
  render(){
    const phenotype1 = this.props.phenotype1;
    if(this.props.phenotype1 == null){
        return <p></p>;
    } else {
        return <div className="card">
                    <h5 className="card-header">colocalization</h5>
	                <div className="card-body">
  	                    <Summary phenotype1={ phenotype1 } />
  	                </div>
               </div>;
    }
  }
};

SummaryCard.propTypes = {
    phenotype1: PropTypes.string
}


export { Summary, SummaryCard }
