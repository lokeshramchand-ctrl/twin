def build_context(
    data
):

    return f"""

Address:

{data.address}

Parcel:

{data.parcel}

Zoning:

{data.zoning}

Flood:

{data.flood}

Fire:

{data.fire}

Schools:

{data.schools}

Roads:

{data.highways}

Question:

{data.question}

Explain everything
about this location.

"""