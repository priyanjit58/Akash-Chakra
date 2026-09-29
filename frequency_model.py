def create_frequency_bands(
    start_frequency=50,
    end_frequency=400,
    number_of_bands=36
):

    step = (
        end_frequency - start_frequency
    ) / number_of_bands

    bands = []

    for i in range(number_of_bands):

        center_frequency = (
            start_frequency
            + step * (i + 0.5)
        )

        bands.append({

            "id": i,

            "center_frequency":
                round(center_frequency, 3)
        })

    return bands