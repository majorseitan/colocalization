import React, { Component } from 'react';
import PropTypes from 'prop-types';

const Value = ({value}) => {
    return (<td className="text-muted">{ `${value}` }</td>)
}

const Colocation = ({colocation}) => {
    return (
	<tr>
	    <Value value={colocation.source1}/>
	    <Value value={colocation.locus_id1}/>
	    <Value value={colocation.phenotype2}/>
	    <Value value={colocation.phenotype2_description}/>
	    <Value value={colocation.clpp}/>
	    <Value value={colocation.clpa}/>
	</tr>
    )
};

class ColocationList extends Component {
    constructor() {
	super()

	this.state = { data : [], loading: true }; }

    async updateColocationList(){
        	if(this.props.phenotype1 != null){
	            const dataRequest = await fetch(`/api/colocation/${this.props.phenotype1}?min_clpa=0.1&sort_by=clpa&order_by=desc`);
                const data = await dataRequest.json();

                if (data) {
                    this.setState({ data: data, loading: false, });
                }
             }
    }

    async componentDidMount() { this.updateColocationList(); }
    async componentDidUpdate() { this.updateColocationList(); }


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
	        { this.state.data.map((c,i) => <Colocation key={i} colocation={ c } />) }
	        </tbody>
        </table>



	}
    }
}


ColocationList.propTypes = {
    phenotype1: PropTypes.string
}
export default ColocationList