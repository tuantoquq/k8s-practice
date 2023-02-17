import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import AuditTable from "./component/AuditTable";
import { useCallback, useState, createContext, useEffect } from "react";
import SearchName from "./component/SearchName";
import Grid from "@mui/material/Grid";
import axios from "../../Api";
import Root from "../../Constant";

export default function Audit() {
    const [rows, setRows] = useState([]);

    const refreshRows = () => {
        var token = localStorage.getItem("token");
        const config = {
            headers: { Authorization: `${token}` },
        };
        axios.get(Root.Audit.GetAll, config).then((res) => {
            var _rows = res.data.map((row, index) => {
                return {
                    audit_id: row.Id,
                    user_id: row.UserId,
                    action:
                        row.Action == 0
                            ? "Create"
                            : row.action == 1
                            ? "Update"
                            : "Delete",
                    action_at: row.ActionAt,
                    miner_id: row.MinerId,
                    name: row.Name,
                    username: row.Username,
                    miner_name: row.MinerName,
                };
            });
            setRows(_rows);
        });
    };
    useEffect(() => {
        refreshRows();
    }, []);
    const [search, setSearch] = useState("");
    return (
        <>
            <Grid container spacing={2} width="100%">
                <Grid item xs={4}>
                    <SearchName search={search} setSearch={setSearch} />
                </Grid>
            </Grid>
            <AuditTable
                rows={rows.filter((row) =>
                    row.username
                        ?.toLowerCase()
                        .includes(search.toLocaleLowerCase())
                )}
            />
        </>
    );
}
