import React, { useState, useEffect , useContext } from 'react';
import PropTypes from 'prop-types';
import ReactTable from 'react-table';
import { SearchContext } from '../contexts/SearchContext';
import axios from 'axios'

const ColocalizationList = (props) => {
    const { phenotype1 } = useContext(SearchContext);
    useEffect( () => {
        getColocalizationList();
    }, [phenotype1]); /* only update on phenotype1 */

    const [colocalizationList, setColocalizationList] = useState(null); /* set up hooks for co*/
    const [filtered, setFiltered] = useState([]);
    function getColocalizationList(){
        if(phenotype1 !== null){
            const url = `/api/colocalization/${phenotype1}?min_clpa=0.1&sort_by=clpa&order_by=desc`;
            axios.get(url).then((d) => { setColocalizationList(d.data); console.log(d.data); } ).catch(function(error){ alert(error);});
        }
    }

    if(phenotype1 == null) {
        return  (<div />);
    } else if(colocalizationList != null){
        const columns = [ { Header: () => (<span title="source" style={{textDecoration: 'underline'}}>Source</span>) ,
                            accessor: "source2" },
                          { Header: () => (<span title="locus id" style={{textDecoration: 'underline'}}>Locus ID</span>) ,
                            accessor: "locus_id1" },
                          { Header: () => (<span title="qlt code" style={{textDecoration: 'underline'}}>QTL code</span>) ,
                            accessor: "phenotype2" },
                          { Header: () => (<span title="qlt" style={{textDecoration: 'underline'}}>QTL</span>) ,
                            accessor: "phenotype2_description" },
                          { Header: () => (<span title="tissue" style={{textDecoration: 'underline'}}>Tissue</span>) ,
                            accessor: "tissue2",
                            Cell: props => (props.value === 'NA' || props.value === '') ? 'NA' : props.value.replace(/_/g,' ') },
                          { Header: () => (<span title="clpp" style={{textDecoration: 'underline'}}>CLPP</span>) ,
                            accessor: "clpp",
                            Cell: props => (props.value === 'NA' || props.value === '') ? 'NA' : props.value.toPrecision(2) },
                          { Header: () => (<span title="clpa" style={{textDecoration: 'underline'}}>CLPA</span>) ,
                            accessor: "clpa" ,
                            Cell: props => (props.value === 'NA' || props.value === '') ? 'NA' : props.value.toPrecision(2)
                            }];

        return (<ReactTable data={ colocalizationList }
                            columns={ columns }
                            defaultSorted={[{  id: "clpa", desc: true }]}
                            defaultPageSize={10}
                            filterable
		                    defaultFilterMethod={(filter, row) => row[filter.id].toLowerCase().startsWith(filter.value)}
		                    onFilteredChange={filtered => { setFiltered({filtered: filtered})}}
		                    className="-striped -highlight"/>);
    } else {
        return (<div>Loading ... </div>);
    }
}


ColocalizationList.propTypes = {
    phenotype1: PropTypes.string
}
export default ColocalizationList
