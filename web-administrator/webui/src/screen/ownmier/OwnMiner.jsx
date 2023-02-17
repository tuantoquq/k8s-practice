import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import MinerTable from "./component/MinerTable";
import { useState, useEffect } from "react";
import SearchName from "./component/SearchName";
import Grid from "@mui/material/Grid";
import axios from "../../Api";
import Root from "../../Constant";
import UpdateCreateMiner from "../component/UpdateCreateMiner";

export default function OwnMiner() {
    const [rows, setRows] = useState([]);
    const [miner, setMiner] = useState({
        CreateAt: "",
        Formula: "",
        GetInputs: "",
        Id: 0,
        InputTables: "",
        IsActive: "",
        IsSuccess: true,
        Name: "",
        RecursiveRange: 0,
        Schedule: "0 0 * * *",
        UpdateAt: "",
    });
    const [noticeCreate, setNoticeCreate] = useState("");
    const [openModalMinerUpdateCreate, setOpenModalMinerUpdateCreate] =
        useState(false);

    const refreshRows = () => {
        var token = localStorage.getItem("token");
        const config = {
            headers: { Authorization: `${token}` },
        };
        axios.get(Root.Miner.GetOwnMiner, config).then((res) => {
            var _rows = res.data.map((row, index) => {
                return {
                    CreateAt: row.CreateAt.substr(0, row.CreateAt.length - 9),
                    IsActive: row.IsActive ? "Yes" : "No",
                    Formula: row.Formula,
                    Name: row.Name,
                    UpdateAt: row.UpdateAt.substr(0, row.CreateAt.length - 9),
                    Id: row.Id,
                    Schedule: row.Schedule,
                    InputTables: row.InputTables,
                    RecursiveRange: row.RecursiveRange,
                    GetInputs: row.GetInputs,
                    IsSuccess: row.IsSuccess,
                };
            });
            setRows(_rows);
        });
    };
    useEffect(() => {
        refreshRows();
    }, []);
    const [search, setSearch] = useState("");
    const onClickCreate = () => {
        var token = localStorage.getItem("token");
        const config = {
            headers: { Authorization: `${token}` },
        };
        let createMiner = {
            Name: miner.Name,
            InputTables: miner.InputTables,
            RecursiveRange: miner.RecursiveRange,
            GetInputs: miner.GetInputs,
            Formula: miner.Formula,
        };
        axios.post(Root.Miner.Create, createMiner, config).then((res) => {
            setNoticeCreate("Create successfully!");
        });
    };
    return (
        <>
            <UpdateCreateMiner
                status={openModalMinerUpdateCreate}
                callBack={() => {
                    setOpenModalMinerUpdateCreate(false);
                    setNoticeCreate("");
                    setMiner({
                        CreateAt: "",
                        Formula: "",
                        GetInputs: "",
                        Id: 0,
                        InputTables: "",
                        IsActive: "",
                        IsSuccess: true,
                        Name: "",
                        RecursiveRange: 0,
                        Schedule: "0 0 * * *",
                        UpdateAt: "",
                    });
                }}
                Miner={miner}
                setValue={setMiner}
                IsCreate={true}
                onClick={onClickCreate}
                notice={noticeCreate}
            />
            <Grid container spacing={2} width="100%">
                <Grid item xs={4}>
                    <SearchName search={search} setSearch={setSearch} />
                </Grid>
            </Grid>
            <MinerTable
                rows={rows.filter((row) =>
                    row.Name?.toLowerCase().includes(search.toLocaleLowerCase())
                )}
            />
            <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
                <Button
                    variant="contained"
                    size="medium"
                    sx={{
                        width: "200px",
                        marginTop: "20px",
                        marginRight: "10px",
                    }}
                    onClick={() => {
                        setOpenModalMinerUpdateCreate(true);
                    }}
                >
                    Add custom miner
                </Button>
            </Box>
        </>
    );
}
