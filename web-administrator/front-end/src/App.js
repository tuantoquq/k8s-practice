import * as React from "react";
import RootRouter from "./navigation";

function App() {
    React.useEffect(() => {
        document.title = 'Master controller';
      }, []);
    return (
        <>
            <RootRouter />
        </>
    );
}

export default App;