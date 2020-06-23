import React, { Component } from 'react';

import './App.css';

class Summary extends Component {
    constructor() {
	super()

	this.state = {
	    data : null,
	    loading: true
	};
    }
    async componentDidMount() {
	const dataRequest = await fetch('/colocation/summary');
    const data = await dataRequest.json();

        if (data) {
            this.setState({
                 data: data,
                 loading: false,
	    });
        }
    }

    render() {
	if(this.state.loading){
	    return <div>Loading ... </div>
	} else {
	    let summary = this.state.data;
	    return (<div>This region has {` ${ summary.count }`} colocations ,
		         unique genes {` ${ summary.unique_phenotype2 }`} ,
		         unique tissues {` ${ summary.unique_tissue2 }`}
		    </div>)
	}
    }
}

const Value = ({value}) => {
    return (<td class="text-muted">{ `${value}` }</td>)
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

class List extends Component {
    constructor() {
	super()

	this.state = {
	    data : [],
	    loading: true
	};
    }
    async componentDidMount() {
	const dataRequest = await fetch('/colocation');
    const data = await dataRequest.json();

        if (data) {
            this.setState({
                 data: data,
                 loading: false,
	    });
        }
    }

    render() {
	if(this.state.loading){
	    return <div>Loading ... </div>
	} else {
	    return this.state.data.map(c => <Colocation key={c.id} colocation={ c } />)
	}
    }
}


function App() {
  return (
    <div>
	 <header></header>
	 <div id="content">
	  <Summary />
          <table class="table">
           <tr>

	            <td>source1</td>

	            <td>locus_id1</td>

        	    <td>phenotype1</td>
	            <td>phenotype1_description</td>

	            <td>clpp</td>
        	    <td>clpa</td>

           </tr>
	   <List />
         </table>
       </div>
    </div>
  );
}

export default App;
