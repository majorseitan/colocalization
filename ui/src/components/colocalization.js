import React, { Component } from 'react';
import PropTypes from 'prop-types';
import NumberFormat from 'react-number-format';
import { chipTableCols } from '../pheweb/tables';
import ReactTable from 'react-table';
import useTable from  'react-table';




const Value = ({value}) => {
    return (<td className="text-muted">{ `${value}` }</td>)
}

const Colocalization = ({colocalization}) => {
    return (
	<tr>
	    <Value value={colocalization.source2}/>
	    <Value value={colocalization.locus_id1}/>
	    <Value value={colocalization.phenotype2}/>
	    <Value value={colocalization.phenotype2_description}/>
	    <Value value={colocalization.tissue2.replace(/_/g,' ')}/>
	    <NumberFormat value={colocalization.clpp} displayType={'text'} decimalScale={2} renderText={value => <td>{value}</td>} />
	    <NumberFormat value={colocalization.clpa} displayType={'text'} decimalScale={2} renderText={value => <td>{value}</td>} />
	</tr>
    )
};

class ColocalizationList extends Component {
    constructor() {
	super();

	this.state = { data: null,
	               columns: [ { Header : "source" , accessor: "source2" },
	                          { Header : "locus id" , accessor: "locus_id1" },
	                          { Header : "QTL code" , accessor: "phenotype1" },
	                          { Header : "QTL" , accessor: "phenotype1_description" },
	                          { Header : "clpp" , accessor: "clpp" },
	                          { Header : "clpa" , accessor: "clpa" } ],
	               dataToDownload: [],
	               filtered: [],
	               headers: [ {label: 'source', key: 'LONGNAME'},
	                          {label: 'locus id', key: 'LONGNAME'},
	                          {label: 'QTL code', key: 'LONGNAME'},
	                          {label: 'QTL', key: 'LONGNAME'},
	                          {label: 'clpp', key: 'LONGNAME'},
	                          {label: 'clpa', key: 'LONGNAME'} ] };

	}

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
    } else if(this.state.data == null){
	    return <div>Loading ... </div>
	} else {

    //return ReactTable(this.state.columns,this.state.data);
	    return <table className="table">
	        <thead>
                   <tr>
	                   <th>source</th>
	                   <th>locus id</th>
                       <th>QTL code</th>
	                   <th>QTL</th>
	                   <th>tissue</th>
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
