import { connect } from 'react-redux';

// Actions
const update_phenotype1 = (phenotype1) => {
    return { type: 'UPDATE_PHENOTYPE1',
             phenotype1 }
}
const update_chromosome = (chromosome) => {
    return { type: 'UPDATE_CHROMOSOME',
             chromosome }
}
const update_start = (start) => {
    return { type: 'UPDATE_START',
             start }
}
const update_stop = (stop) => {
    return { type: 'UPDATE_STOP',
             stop }
}
/* Query a region an a phenotype
 */
const start_state = { phenotype1 : null,
                      chromosome : null,
                      start : null,
                      stop : null};
// Reducer

/* Reducer
 * The role is to build up the state for the query
 * by updating the state.
 */
const search_parameters = (state = start_state,action) => {
    switch(action.type){
        case 'UPDATE_PHENOTYPE1' :
            return { ...state, phenotype1 : action.phenotype1 };

        case 'UPDATE_CHROMOSOME' :
            return { ...state, chromosome : action.chromosome };

        case 'UPDATE_START' :
            return { ...state, start : action.start };

        case 'UPDATE_STOP' :
           return { ...state, stop : action.stop };

        default:
            return state;
    }
}
/* Just a pass through that clones,
 * the state.
 */
function mapStateToProps(state) {
  return { ...state };
};

function mapDispatchToProps(dispatch){
    return { update_phenotype1 : (phenotype1) => dispatch(update_phenotype1(phenotype1)) ,
             update_chromosome : (chromosome) => dispatch(update_chromosome(chromosome)) ,
             update_start : (start) => dispatch(update_start(start)) ,
             update_stop : (stop) => dispatch(update_stop(stop)) };
};

const connector = connect(mapStateToProps,mapDispatchToProps);

export { search_parameters , connector }
