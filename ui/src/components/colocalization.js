import React, { useState, useEffect , useContext } from 'react';
import PropTypes from 'prop-types';
import NumberFormat from 'react-number-format';
import { useTable } from 'react-table';
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

const Table = ({ columns, data }) => {
  const { getTableProps,
          getTableBodyProps,
          headerGroups,
          rows,
          prepareRow } = useTable({ columns, data });

  return (
    <table {...getTableProps()}>
      <thead>
        {headerGroups.map(headerGroup => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map(column => (
              <th {...column.getHeaderProps()}>{column.render("Header")}</th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody {...getTableBodyProps()}>
        {rows.map((row, i) => {
          prepareRow(row);
          return (
            <tr {...row.getRowProps()}>
              {row.cells.map(cell => {
                return <td {...cell.getCellProps()}>{cell.render("Cell")}</td>;
              })}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
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
            axios.get(url).then((d) => { setCocalizationList(d.data); console.log(d.data); /**/ } ).catch(function(error){ alert(error);});
        }
    }

    if(phenotype1 == null) {
        return  <div />;
    } else if(colocalizationList != null){
        const columns = [ { Header: "source", accessor: "source2" },
                          { Header: "locus id", accessor: "locus_id1" },
                          { Header: "QTL code", accessor: "phenotype2" },
                          { Header: "QTL", accessor: "phenotype2_description" },
                          { Header: "tissue", accessor: "tissue2" },
                          { Header: "clpp", accessor: "clpp" },
                          { Header: "clpa", accessor: "clpa" }];

        return <Table data={colocalizationList} columns={columns} />;
    } else {
        return (<div>Loading ... </div>);
    }
}


ColocalizationList.propTypes = {
    phenotype1: PropTypes.string
}
export default ColocalizationList
