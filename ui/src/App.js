import React, { Component } from 'react';

import './App.css';

const Value = ({value}) => {
    return (
	    <td>{ `${value}` }</td>
    )
}

const Colocation = ({colocation}) => {
    return (
	<tr>
	    <Value value={colocation.source1}/>
	    <Value value={colocation.source2}/>

	    <Value value={colocation.phenotype1}/>
	    <Value value={colocation.phenotype1_description}/>
	    <Value value={colocation.phenotype2}/>
	    <Value value={colocation.phenotype2_description}/>

	    <Value value={colocation.tissue1}/>
	    <Value value={colocation.tissue2}/>
	    <Value value={colocation.locus_id1}/>
	    <Value value={colocation.locus_id2}/>

	    <Value value={colocation.chromosome}/>
	    <Value value={colocation.start}/>
	    <Value value={colocation.stop}/>

	    <Value value={colocation.clpp}/>
	    <Value value={colocation.clpa}/>
	    <Value value={colocation.beta_id1}/>
	    <Value value={colocation.beta_id2}/>

	    <Value value={colocation.variation}/>
	    <Value value={colocation.vars_pip1}/>
	    <Value value={colocation.vars_pip2}/>
	    <Value value={colocation.vars_beta1}/>
	    <Value value={colocation.vars_beta2}/>

	    <Value value={colocation.len_cs1}/>
	    <Value value={colocation.len_cs2}/>
	    <Value value={colocation.len_inter}/>
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
	const data = await fetch('/colocation');
        const dataJSON = await data.json();

        if (dataJSON) {
            this.setState({
                 data: dataJSON,
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
          <table class="table">
           <tr>
	    <td>source1</td>
	    <td>source2</td>

	    <td>phenotype1</td>
	    <td>phenotype1_description</td>
	    <td>phenotype2</td>
	    <td>phenotype2_description</td>

	    <td>tissue1</td>
	    <td>tissue2</td>
	    <td>locus_id1</td>
	    <td>locus_id2</td>

	    <td>chromosome</td>
	    <td>start</td>
	    <td>stop</td>

	    <td>clpp</td>
	    <td>clpa</td>
	    <td>beta_id1</td>
	    <td>beta_id2</td>

	    <td>variation</td>
	    <td>vars_pip1</td>
	    <td>vars_pip2</td>
	    <td>vars_beta1</td>
	    <td>vars_beta2</td>

	    <td>len_cs1</td>
	    <td>len_cs2</td>
	    <td>len_inter</td>
           </tr>
	   <List />
         </table>
       </div>
    </div>
  );
}

export default App;
