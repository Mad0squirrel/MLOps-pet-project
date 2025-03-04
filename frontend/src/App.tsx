import maplibregl from 'maplibre-gl';
import { useEffect } from 'react';

const App = () => {
    useEffect(() => {
        const map = new maplibregl.Map({
            container: 'map',
            style: 'https://api.maptiler.com/maps/basic-v2/style.json?key=bLQ9PLUtNvDYbN6lEQDA',
            center: [37.6173, 55.7558],
            zoom: 10
        });

        return () => map.remove();
    }, []);

    return <div id="map" style={{ width: "100vw", height: "100vh" }} />;
};

export default App;

