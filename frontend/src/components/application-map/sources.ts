import {apartmentsDataPath, apartmentsSourceId} from "./constants.ts";
import {SourceSpecification} from "maplibre-gl";


type sourceSpec = () => [string, SourceSpecification];

const createApartmentsSourceSpec: sourceSpec = () => {
    return  [
        apartmentsSourceId,
        {
            type: "geojson",
            data: apartmentsDataPath,
        }
    ]
}


export {createApartmentsSourceSpec};