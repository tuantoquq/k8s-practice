import * as React from "react";
import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import DetailMiner from "../../component/DetailMiner";
import UpdateCreateMiner from "../../component/UpdateCreateMiner";
import Root from "../../../Constant";
import axios from "../../../Api";
import ConfirmModal from "../../component/ConfirmModal";
import { Modal, Box } from "@mui/material";
import { styled } from "@mui/material/styles";
import { tableCellClasses } from "@mui/material/TableCell";
import CodeIcon from "@mui/icons-material/Code";

const StyledTableCell = styled(TableCell)(({ theme }) => ({
    [`&.${tableCellClasses.head}`]: {
        backgroundColor: theme.palette.primary.main,
        color: theme.palette.common.white,
    },
    [`&.${tableCellClasses.body}`]: {
        fontSize: 14,
    },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
    "&:nth-of-type(odd)": {
        backgroundColor: theme.palette.action.hover,
    },
    // hide last border
    "&:last-child td, &:last-child th": {
        border: 0,
    },
}));

const columns = [
    {
        id: "Id",
        label: "Id",
        minWidth: 60,
        align: "center",
    },
    {
        id: "Name",
        label: "Name",
        minWidth: 60,
        align: "center",
    },
    {
        id: "Schedule",
        label: "Schedule",
        minWidth: 60,
        align: "center",
    },
    {
        id: "CreateAt",
        label: "Create At",
        minWidth: 60,
        align: "center",
    },
    {
        id: "UpdateAt",
        label: "Update At",
        minWidth: 60,
        align: "center",
    },
    {
        id: "NameDefineUser",
        label: "Name Define User",
        minWidth: 60,
        align: "center",
    },
    {
        id: "Username",
        label: "Username",
        minWidth: 60,
        align: "center",
    },
    {
        id: "actions",
        label: "",
        minWidth: 60,
        align: "center",
    },
];

function MinerTable(props) {
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(10);
    const [openModalMinerMethod, setOpenModalMinerMethod] =
        React.useState(false);
    const [openModalMinerUpdateCreate, setOpenModalMinerUpdateCreate] =
        React.useState(false);
    const [openModalDeleteConfirm, setOpenModalDeleteConfirm] =
        React.useState(false);
    const [isCreate, setIsCreate] = React.useState(false);
    const [miner, setMiner] = React.useState({});
    const [noticeUpdate, setNoticeUpdate] = React.useState("");
    const rows = props.rows;

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(+event.target.value);
        setPage(0);
    };

    const handleRow = (Miner) => {
        setOpenModalMinerMethod(true);
        setMiner(Miner);
    };

    const onClickUpdate = () => {
        var token = localStorage.getItem("token");
        const config = {
            headers: { Authorization: `${token}` },
        };
        axios.post(Root.Miner.UpdateDefault, miner, config).then((res) => {
            setNoticeUpdate("Update successfully!");
        });
    };

    const onClickDelete = () => {
        var token = localStorage.getItem("token");
        const config = {
            headers: { Authorization: `${token}` },
        };
        axios.post(Root.Miner.DeleteDefault, miner, config).then((res) => {
            window.location.reload();
        });
    };
    return (
        <>
            <Paper sx={{ width: "100%", overflow: "hidden" }}>
                <TableContainer sx={{ maxHeight: 440 }}>
                    <Table stickyHeader aria-label="sticky table">
                        <TableHead>
                            <StyledTableRow>
                                {columns.map((column) => (
                                    <StyledTableCell
                                        key={column.id}
                                        align={column.align}
                                        style={{ minWidth: column.minWidth }}
                                    >
                                        {column.label}
                                    </StyledTableCell>
                                ))}
                            </StyledTableRow>
                        </TableHead>
                        <TableBody>
                            {rows
                                .slice(
                                    page * rowsPerPage,
                                    page * rowsPerPage + rowsPerPage
                                )
                                .map((row) => {
                                    return (
                                        <StyledTableRow
                                            hover
                                            role="checkbox"
                                            tabIndex={-1}
                                            key={row.code}
                                        >
                                            {columns.map((column) => {
                                                if (column.id !== "actions") {
                                                    const value =
                                                        row[column.id];
                                                    return (
                                                        <StyledTableCell
                                                            key={column.id}
                                                            align={column.align}
                                                        >
                                                            {column.format &&
                                                            typeof value ===
                                                                "number"
                                                                ? column.format(
                                                                      value
                                                                  )
                                                                : value}
                                                        </StyledTableCell>
                                                    );
                                                } else {
                                                    return (
                                                        <StyledTableCell
                                                            key={column.id}
                                                            align={column.align}
                                                        >
                                                            <Stack
                                                                spacing={2}
                                                                direction="row"
                                                            >
                                                                <Button
                                                                    variant="outlined"
                                                                    startIcon={
                                                                        <CodeIcon />
                                                                    }
                                                                    onClick={() => {
                                                                        handleRow(
                                                                            row
                                                                        );
                                                                    }}
                                                                >
                                                                    Source code
                                                                </Button>
                                                                {row.UserCanUse ==
                                                                    "all" && (
                                                                    <>
                                                                        <Button
                                                                            variant="outlined"
                                                                            startIcon={
                                                                                <EditIcon />
                                                                            }
                                                                            onClick={() => {
                                                                                setMiner(
                                                                                    row
                                                                                );
                                                                                setOpenModalMinerUpdateCreate(
                                                                                    true
                                                                                );
                                                                                setIsCreate(
                                                                                    false
                                                                                );
                                                                            }}
                                                                        >
                                                                            Edit
                                                                        </Button>

                                                                        <Button
                                                                            variant="outlined"
                                                                            startIcon={
                                                                                <DeleteIcon />
                                                                            }
                                                                            onClick={() => {
                                                                                setMiner(
                                                                                    row
                                                                                );
                                                                                setOpenModalDeleteConfirm(
                                                                                    true
                                                                                );
                                                                            }}
                                                                        >
                                                                            Delete
                                                                        </Button>
                                                                    </>
                                                                )}
                                                            </Stack>
                                                        </StyledTableCell>
                                                    );
                                                }
                                            })}
                                        </StyledTableRow>
                                    );
                                })}
                        </TableBody>
                    </Table>
                </TableContainer>
                <TablePagination
                    rowsPerPageOptions={[10, 25, 100]}
                    component="div"
                    count={rows.length}
                    rowsPerPage={rowsPerPage}
                    page={page}
                    onPageChange={handleChangePage}
                    onRowsPerPageChange={handleChangeRowsPerPage}
                />
            </Paper>
            <DetailMiner
                status={openModalMinerMethod}
                callBack={() => {
                    setOpenModalMinerMethod(false);
                }}
                Miner={miner}
                setValue={setMiner}
            />
            <UpdateCreateMiner
                status={openModalMinerUpdateCreate}
                callBack={() => {
                    setOpenModalMinerUpdateCreate(false);
                    setNoticeUpdate("");
                }}
                Miner={miner}
                setValue={setMiner}
                IsCreate={isCreate}
                onClick={onClickUpdate}
                notice={noticeUpdate}
            />
            <ConfirmModal
                status={openModalDeleteConfirm}
                callBack={() => setOpenModalDeleteConfirm(false)}
                onClick={onClickDelete}
                title={"Do you want to delete miner " + miner.Name}
            />
        </>
    );
}

export default React.memo(MinerTable);
