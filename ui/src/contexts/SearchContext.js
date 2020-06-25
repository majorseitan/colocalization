import React, { createContext,  Component } from 'react';

export const SearchContext = createContext();


class SearchContextProvider extends Component {
    state = { phenotype1 : null,
              chromosome : null,
              start : null,
              stop : null }
    render() {
        return (<SearchContext.Provider value={{...this.state ,
                                                updatePhenotype : this.updatePhenotype ,
                                                updateChromosome :  this.updateChromosome ,
                                                updateStart : this.updateStart ,
                                                updateStop : this.updateStop }}>
                {this.props.children}
                </SearchContext.Provider>);
    }

    updatePhenotype = (phenotype1) => {
        this.setState({ phenotype1 });
    }

    updateChromosome = (chromosome) => {
        this.setState({ chromosome });
    }

    updateStart = (start) => {
        this.setState({ start });
    }

    updateStop = (stop) => {
        this.setState({ stop });
    }

};

export default SearchContextProvider;