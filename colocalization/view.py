from flask import Blueprint
from colocalization.model import list_phenotype1, load_phenotype1, list_colocalization, summary_colocalization, locus_colocalization
from colocalization.model import load_phenotype1

colocalization = Blueprint('colocalization', __name__)

@colocalization.route('/api/colocalization/<string:phenotype1>/<int:chromosome>:<int:start>-<int:stop>', methods=["GET"])
def do_list_colocalization(phenotype1: str,
                           chromosome: int,
                           start: int,
                           stop: int):
    return json.dumps(list_colocalization(phenotype1,
                                          chromosome,
                                          start,
                                          stop,
                                          min_clpa=get_min_clpa(),
                                          sort_by=get_sort_by(),
                                          desc=get_desc()))


@colocalization.route('/api/colocalization/<string:phenotype1>/<int:chromosome>:<int:start>-<int:stop>/summary', methods=["GET"])
def do_summary_colocalization(phenotype1: str,
                              chromosome: int,
                              start: int,
                              stop: int):
    return json.dumps(summary_colocalization(phenotype1,
                                             chromosome,
                                             start,
                                             stop,
                                             min_clpa=get_min_clpa()))


@colocalization.route('/api/colocalization/<string:phenotype1>/locus_id/<string:locus_id1>', methods=["GET"])
def do_locus_colocalization(phenotype1: str,locus_id1: str):
    return json.dumps(locus_colocalization(phenotype1,
                                           locus_id1,
                                           min_clpa = get_min_clpa()))

development = Blueprint('development', __name__)
@development.route('/api/colocalization', methods=["POST"])
def post_phenotype1():
    f = request.files['csv']
    path = secure_filename(f.filename)
    path = os.path.join(upload_dir, path)
    f.save(path)
    return json.dumps(load_phenotype1(path))
