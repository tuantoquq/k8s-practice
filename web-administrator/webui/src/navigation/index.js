import { Route, Routes } from "react-router-dom";
import AdminLayout from "../layout/AdminLayout";
import UserLayout from "../layout/UserLayout";
import Audit from "../screen/audit/Audit";
import Login from "../screen/login/Login";
import Miner from "../screen/miner/Miner";
import Data from "../screen/data/Data";
import OwnMiner from "../screen/ownmier/OwnMiner";

export default function RootRouter() {
    return (
        <>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/" element={<AdminLayout />}>
                    <Route path="audit" element={<Audit />} />
                    <Route path="miner" element={<Miner />} />
                </Route>
                <Route path="/" element={<UserLayout />}>
                    <Route path="data" element={<Data />} />
                    <Route path="ownminer" element={<OwnMiner />} />
                </Route>
            </Routes>
        </>
    );
}
