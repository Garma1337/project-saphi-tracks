import Box from "@mui/material/Box/Box";

interface TabContentProps {
    children: React.ReactNode;
    value: number;
    index: number;
}

const TabContent = (props: TabContentProps) => {
    const {children, value, index, ...other} = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && <Box sx={{py: 2}}>{children}</Box>}
        </div>
    );
}

export default TabContent;