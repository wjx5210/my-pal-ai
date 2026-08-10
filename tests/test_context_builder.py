from app.context_builder import build_hybrid_context


def test_build_context():

    result = {
        "entities":[
            {
                "name":"棉悠悠"
            }
        ],

        "rag_contexts":[
            {
                "text":"前期基地推荐捣蛋猫"
            }
        ]
    }


    context = build_hybrid_context(result)


    assert len(context["entities"]) == 1
    assert len(context["knowledge"]) == 1