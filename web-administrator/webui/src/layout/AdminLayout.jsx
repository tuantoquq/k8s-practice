import { Outlet } from "react-router-dom";
import * as React from "react";
import { useEffect } from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import ButtonGroup from "@mui/material/ButtonGroup";
import ClickAwayListener from "@mui/material/ClickAwayListener";
import Grow from "@mui/material/Grow";
import Paper from "@mui/material/Paper";
import Popper from "@mui/material/Popper";
import MenuItem from "@mui/material/MenuItem";
import MenuList from "@mui/material/MenuList";
import MenuIcon from "@mui/icons-material/Menu";
import { useNavigate } from "react-router-dom";

const options = ["Audit", "Miner", "Log out"];

function SplitButton() {
    const [open, setOpen] = React.useState(false);
    const anchorRef = React.useRef(null);
    const [selectedIndex, setSelectedIndex] = React.useState(
        localStorage.getItem("selectedIndex") || 0
    );
    const navigate = useNavigate();
    useEffect(() => {
        navigateTo();
    }, [selectedIndex]);

    const handleMenuItemClick = (event, index) => {
        setSelectedIndex(index);
        setOpen(false);
        localStorage.setItem("selectedIndex", selectedIndex);
    };

    const handleToggle = () => {
        setOpen((prevOpen) => !prevOpen);
    };

    const handleClose = (event) => {
        if (anchorRef.current && anchorRef.current.contains(event.target)) {
            return;
        }
        setOpen(false);
    };

    const navigateTo = () => {
        if (selectedIndex === undefined) return;
        if (selectedIndex === 0) navigate("/audit");
        if (selectedIndex === 1) navigate("/miner");
        if (selectedIndex === 2) {
            navigate("/");
            localStorage.removeItem("selectedIndex");
            localStorage.removeItem("token");
        }
    };

    return (
        <React.Fragment>
            <ButtonGroup
                variant="contained"
                ref={anchorRef}
                aria-label="split button"
            >
                <Button
                    size="small"
                    aria-controls={open ? "split-button-menu" : undefined}
                    aria-expanded={open ? "true" : undefined}
                    aria-label="select merge strategy"
                    aria-haspopup="menu"
                    onClick={handleToggle}
                >
                    <MenuIcon />
                </Button>
            </ButtonGroup>
            <Popper
                sx={{
                    zIndex: 1,
                }}
                open={open}
                anchorEl={anchorRef.current}
                role={undefined}
                transition
                disablePortal
            >
                {({ TransitionProps, placement }) => (
                    <Grow
                        {...TransitionProps}
                        style={{
                            transformOrigin:
                                placement === "bottom"
                                    ? "center top"
                                    : "center bottom",
                        }}
                    >
                        <Paper>
                            <ClickAwayListener onClickAway={handleClose}>
                                <MenuList id="split-button-menu" autoFocusItem>
                                    {options.map((option, index) => (
                                        <MenuItem
                                            key={option}
                                            selected={index === selectedIndex}
                                            onClick={(event) =>
                                                handleMenuItemClick(
                                                    event,
                                                    index
                                                )
                                            }
                                        >
                                            {option}
                                        </MenuItem>
                                    ))}
                                </MenuList>
                            </ClickAwayListener>
                        </Paper>
                    </Grow>
                )}
            </Popper>
        </React.Fragment>
    );
}

function Header() {
    return (
        <Box sx={{ flexGrow: 1, zIndex: 999 }}>
            <AppBar position="static" sx={{ boxShadow: "none" }}>
                <Toolbar>
                    <Typography
                        variant="h6"
                        component="div"
                        sx={{ flexGrow: 1 }}
                    >
                        Master Controller
                    </Typography>
                    <SplitButton />
                </Toolbar>
            </AppBar>
        </Box>
    );
}

export default function AdminLayout() {
    return (
        <div style={{ display: "flex", flexDirection: "column" }}>
            <Header />
            <Outlet />
        </div>
    );
}