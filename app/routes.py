from flask import render_template, Blueprint, redirect

from .forms import ViewerForm
from .models import Keyphrase, Text
from .keyphrase_parser import get_keyphrases

viewer_blueprint = Blueprint("viewer_blueprint", __name__)


@viewer_blueprint.route("/", methods=["GET", "POST"])
def viewer():
    form = ViewerForm()

    text_obj = None

    if form.validate_on_submit():
        text_id = Text.get_text_id_by_text(form.text.data)

        if text_id:
            return redirect(f"/{text_id}")
        else:
            text_obj = Text.create(form.text.data)

            keyphrases = get_keyphrases(form.text.data)

            for keyphrase in keyphrases:
                keyphrase_exists = Keyphrase.get_keyphrase_obj(keyphrase["keyphrase"])

                if keyphrase_exists:
                    text_obj.append_keyphrase(keyphrase_exists)
                else:
                    keyphrase_obj = Keyphrase.create(keyphrase)

                    text_obj.append_keyphrase(keyphrase_obj)

    return render_template("viewer.html", form=form, text=text_obj)


@viewer_blueprint.route("/saved_texts", methods=["GET"])
@viewer_blueprint.route("/<int:text_id>", methods=["GET"])
def saved_texts(text_id=None):
    form = ViewerForm()

    text_obj = None

    if text_id:
        text_obj = Text.get_text_obj_by_id(text_id)
        form.text.data = text_obj.text

    return render_template(
        "saved_texts.html", form=form, text=text_obj, texts=Text.get_all()
    )


@viewer_blueprint.route("/top", methods=["GET"])
def top_keyphrases():
    return render_template(
        "top_keyphrases.html",
        keyphrases=Keyphrase.top_keyphrases(),
    )
