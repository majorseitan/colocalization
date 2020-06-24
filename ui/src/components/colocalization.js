import React, { Component } from 'react';
import PropTypes from 'prop-types';

const Value = ({value}) => {
    return (<td className="text-muted">{ `${value}` }</td>)
}

const Colocalization = ({colocalization}) => {
    return (
	<tr>
	    <Value value={colocalization.source1}/>
	    <Value value={colocalization.locus_id1}/>
	    <Value value={colocalization.phenotype2}/>
	    <Value value={colocalization.phenotype2_description}/>
	    <Value value={colocalization.clpp}/>
	    <Value value={colocalization.clpa}/>
	</tr>
    )
};

class ColocalizationList extends Component {
    constructor() {
	super()

	this.state = { data : [], loading: true }; }

    async updateColocalizationList(){
        	if(this.props.phenotype1 != null){
	            const dataRequest = await fetch(`/api/colocalization/${this.props.phenotype1}?min_clpa=0.1&sort_by=clpa&order_by=desc`);
                const data = await dataRequest.json();

                if (data) {
                    this.setState({ data: data, loading: false, });
                }
             }
    }

    async componentDidMount() { this.updateColocalizationList(); }
    async componentDidUpdate() { this.updateColocalizationList(); }


    render() {
	if(this.props.phenotype1 == null){
        return <div/>
    } else if(this.state.loading){
	    return <div>Loading ... </div>
	} else {
	    return <table className="table">
	        <thead>
                   <tr>
	                   <th>source1</th>
	                   <th>locus_id1</th>
                       <th>phenotype1</th>
	                   <th>phenotype1_description</th>
	                   <th>clpp</th>
                       <th>clpa</th>
                   </tr>
	        </thead>
	        <tbody>
	        { this.state.data.map((c,i) => <Colocalization key={i} colocalization={ c } />) }
	        </tbody>
        </table>



	}
    }
}


ColocalizationList.propTypes = {
    phenotype1: PropTypes.string
}
export default ColocalizationList
