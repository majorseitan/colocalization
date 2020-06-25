import React, { Component , useState, useEffect , useContext } from 'react';
import PropTypes from 'prop-types';
import NumberFormat from 'react-number-format';
import { chipTableCols } from '../pheweb/tables';
import ReactTable from 'react-table';
import useTable from  'react-table';
import { SearchContext } from '../contexts/SearchContext';
import axios from 'axios'

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

const ColocalizationList = (props) => {
    const { phenotype1 } = useContext(SearchContext);
    useEffect( () => {
        getCocalizationList();
    });
    const [colocalizationList, setCocalizationList] = useState(null);

    function getCocalizationList(){
        if(phenotype1 !== null){
            const url = `/api/colocalization/${phenotype1}?min_clpa=0.1&sort_by=clpa&order_by=desc`;
            axios.get(url).then(({data}) => { setCocalizationList(data) } ).catch(function(error){ alert(error);})
        }
    }

    if(phenotype1 == null) {
        return  <div/>;
    } else if(colocalizationList != null){
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
	            { colocalizationList.map((c,i) => <Colocalization key={i} colocalization={ c } />) }
	            </tbody>
        </table>
    } else {
        return (<div>Loading ... </div>);
    }
}


ColocalizationList.propTypes = {
    phenotype1: PropTypes.string
}
export default ColocalizationList
