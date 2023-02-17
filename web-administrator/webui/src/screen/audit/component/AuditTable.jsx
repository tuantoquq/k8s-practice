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
import { TextField, Modal, Box } from "@mui/material";
import { styled } from "@mui/material/styles";
import { tableCellClasses } from "@mui/material/TableCell";
import PriorityHighRoundedIcon from "@mui/icons-material/PriorityHighRounded";
import axios from "../../../Api";
import Root from "../../../Constant";
const style = {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: 400,
    bgcolor: "background.paper",
    border: "2px solid #000",
    boxShadow: 24,
    p: 4,
};

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
        id: "audit_id",
        label: "Audit ID",
        minWidth: 60,
        align: "center",
    },
    {
        id: "user_id",
        label: "User ID",
        minWidth: 60,
        align: "center",
    },
    {
        id: "action",
        label: "Action",
        minWidth: 60,
        align: "center",
    },
    {
        id: "action_at",
        label: "Action At",
        minWidth: 60,
        align: "center",
    },
    {
        id: "miner_id",
        label: "Miner ID",
        minWidth: 60,
        align: "center",
    },
    {
        id: "name",
        label: "Name",
        minWidth: 60,
        align: "center",
    },
    {
        id: "username",
        label: "Username",
        minWidth: 60,
        align: "center",
    },
    {
        id: "miner_name",
        label: "MinerName",
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

function AuditTable(props) {
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(10);
    const [openModalUserInformation, setOpenModalUserInformation] =
        React.useState(false);
    const [userInformation, setUserInformation] = React.useState({
        Name: "",
        Username: "",
        Role: "",
        IsActive: "",
        Notice: "",
        UserId: "",
    });
    const rows = props.rows;

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(+event.target.value);
        setPage(0);
    };

    const handleRow = (userId) => {
        var token = localStorage.getItem("token");
        const config = {
            headers: { Authorization: `${token}` },
        };
        axios.get(Root.User.GetUser + userId, config).then((res) => {
            var userInfor = {
                Name: res.data[0].Name,
                Username: res.data[0].Username,
                Role: res.data[0].Role == 0 ? "Admin" : "User",
                IsActive: res.data[0].IsActive == 0 ? "No" : "Yes",
                Notice: "",
                UserId: userId,
            };
            setUserInformation(userInfor);
            setOpenModalUserInformation(true);
        });
    };

    const handleClickLock = (userId) => {
        var token = localStorage.getItem("token");
        const config = {
            headers: { Authorization: `${token}` },
        };
        axios.get(Root.User.Lock + userId, config).then((res) => {
            setUserInformation((prevUser) => {
                return {
                    ...prevUser,
                    Notice: "Lock user succesfully!",
                    IsActive: "No",
                };
            });
        });
    };

    const handleClickUnlock = (userId) => {
        var token = localStorage.getItem("token");
        const config = {
            headers: { Authorization: `${token}` },
        };
        axios.get(Root.User.Unlock + userId, config).then((res) => {
            setUserInformation((prevUser) => {
                return {
                    ...prevUser,
                    Notice: "Unlock user succesfully!",
                    IsActive: "Yes",
                };
            });
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
                                                            <Button
                                                                variant="outlined"
                                                                startIcon={
                                                                    <PriorityHighRoundedIcon />
                                                                }
                                                                onClick={() => {
                                                                    handleRow(
                                                                        row.user_id
                                                                    );
                                                                }}
                                                            >
                                                                Information
                                                            </Button>
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
            <Modal
                open={openModalUserInformation}
                onClose={() => {
                    setOpenModalUserInformation(false);
                    setUserInformation({
                        Name: "",
                        Username: "",
                        Role: "",
                        IsActive: "",
                        UserId: "",
                    });
                }}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={style}>
                    <TextField
                        required
                        id="outlined-required"
                        label="Name"
                        value={userInformation.Name}
                        InputProps={{
                            readOnly: true,
                        }}
                        sx={{ width: "400px", marginBottom: "20px" }}
                    />
                    <TextField
                        required
                        id="outlined-required"
                        label="Username"
                        value={userInformation.Username}
                        InputProps={{
                            readOnly: true,
                        }}
                        sx={{ width: "400px", marginBottom: "20px" }}
                    />
                    <TextField
                        required
                        id="outlined-required"
                        label="Role"
                        value={userInformation.Role}
                        InputProps={{
                            readOnly: true,
                        }}
                        sx={{ width: "400px", marginBottom: "20px" }}
                    />
                    <TextField
                        required
                        id="outlined-required"
                        label="Is Active"
                        value={userInformation.IsActive}
                        InputProps={{
                            readOnly: true,
                        }}
                        sx={{ width: "400px", marginBottom: "20px" }}
                    />
                    <div>{userInformation.Notice}</div>
                    {userInformation.Role == "User" && (
                        <Button
                            sx={{ marginLeft: "150px" }}
                            onClick={() => {
                                userInformation.IsActive == "Yes"
                                    ? handleClickLock(userInformation.UserId)
                                    : handleClickUnlock(userInformation.UserId);
                            }}
                        >
                            {userInformation.IsActive == "Yes"
                                ? "Lock"
                                : "Unlock"}
                        </Button>
                    )}
                </Box>
            </Modal>
        </>
    );
}

export default React.memo(AuditTable);
