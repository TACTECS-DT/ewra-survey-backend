$(document).ready(function () {
    let last_report_data = null;

    $("#get_survey_report_data").click(function () {
        let survey_id =$("#survey_id").val()
        if (!survey_id){
            alert("plese choose a survey ")
        }
        $.ajax({
            url: "/api/get_survey_report_data/?survey_id=" + survey_id,
            type: "GET",
            contentType: "application/json",
        
            success: function (response) {
                if (response.success) {
                    if (response.reports_data){
                        
                        add_report_data(response.reports_data,response.average_main_percentage ,response.total_main_total,response.average_total_main_total_percentage ,response.total_main_full_mark)
                    }
              
                } else {
                    alert("Error: " + (response.error || "Unknown error"));
                }
            },
            error: function (xhr) {
                alert("Request failed: " + xhr.responseText);
            }
        });
    });




    function add_report_data(data ,average_main_percentage ,total_main_total,average_total_main_total_percentage ,total_main_full_mark) {

        total_main_total = Number(total_main_total).toFixed(4)
        total_main_full_mark = Number(total_main_full_mark).toFixed(4)
        average_main_percentage = Number(average_main_percentage).toFixed(4)
        average_total_main_total_percentage = Number(average_total_main_total_percentage).toFixed(4)
        const parent_div = $('.survey_report_data');
        parent_div.empty();
         last_report_data =   data; 

        let sectionIndex = 0;
        // <p>Average Total Percentage: <span class="percentage">%${average_main_percentage}</span></p>
        // <p>Total KPI Score: <span class="value">${total_main_total}</span></p>
        // <p>Total Full Mark: <span class="value">${total_main_full_mark}</span></p>
        let ex_button = `
        <div style="text-align: right; margin-bottom: 10px;">
                 <button id="export_excel" class="btn btn-success">📥 Export to Excel</button>
<br>
<br><br>
<div class="card-container "id='sub_info'>
    <div class="report-card">

    
        <p>Average Total KPI Percentage: <span class="percentage">%${average_total_main_total_percentage}</span></p>
    </div>
</div>

             </div>`
             console.log(data)
         parent_div.append(ex_button);
        for (const [mainSection, mainData] of Object.entries(data)) {
            sectionIndex++;
    
            const mainSectionId = `main_section_${sectionIndex}`;
            const mainPercentage = mainData.main_percentage.toFixed(4);
    
            const mainHeader =  `
 
        <div class="card my-3 shadow">
                    <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center" data-bs-toggle="collapse" href="#${mainSectionId}" role="button">
                        <div>
                            <h5 class="mb-1">${mainSection}</h5>
                            ${renderPercentageBar(mainPercentage, "main")}
                            <small>الإجمالي: ${mainData.main_total.toFixed(4)} / ${mainData.main_full_mark.toFixed(4)}</small>
                        </div>
                        <span class="badge bg-light text-dark">انقر للتوسيع</span>
                    </div>
                    <div id="${mainSectionId}" class="collapse">
                        <div class="card-body">
                            ${renderSubSections(mainData.sub_sections, sectionIndex)}
                        </div>
                    </div>
                </div>
            `;
            parent_div.append(mainHeader);


            $("#export_excel").off("click").on("click", function () {
    
                if (last_report_data) {
                    exportToExcel(last_report_data); // You need to define this function
                } else {
                    alert("No data to export.");
                }
            });

        }
    }
    
    function renderSubSections(subSections, mainIndex) {
        let html = "";
        let subIndex = 0;
    
        for (const [subName, subData] of Object.entries(subSections)) {
            subIndex++;
            const subId = `sub_section_${mainIndex}_${subIndex}`;
            const subPercentage = subData.sub_percentage.toFixed(4);
    
            html += `
                <div class="card mb-3 border-secondary">
                    <div class="card-header bg-secondary text-white d-flex justify-content-between align-items-center" data-bs-toggle="collapse" href="#${subId}" role="button">
                        <div>
                            <h6 class="mb-1">${subName}</h6>
                            ${renderPercentageBar(subPercentage, "sub")}
                            <small>الإجمالي: ${subData.sub_total.toFixed(4)} / ${subData.sub_full_mark.toFixed(4)}</small>
                        </div>
                        <span class="badge bg-light text-dark">انقر للتوسيع</span>
                    </div>
                    <div id="${subId}" class="collapse">
                        <div class="card-body">
                            ${renderQuestions(subData.questions)}
                        </div>
                    </div>
                </div>
            `;
        }
    
        return html;
    }
    
    function renderQuestions(questions) {
        let html = `
            <div class="table-responsive">
            <table class="table table-bordered table-sm">
                <thead class="table-light">
                    <tr>
                        <th>السؤال</th>
                        <th>المؤشر</th>
                        <th> الدرجة</th>
                        <th>المجموع الفرعي</th>
                        <th>ملاحظات</th>
                        <th>توصيات</th>
                    </tr>
                </thead>
                <tbody>
        `;
    
        for (const q of questions) {
            // <td> ${q.is_NA === 'true' ? 'N/A' : q.answer_percentage.toFixed(4)} </td>     
            // 
            html += `
                <tr>
                    <td>${q.question}</td>
                    <td>${q.kpi.toFixed(4)}</td>
                
<td>${q.answer_percentage.toFixed(4)}</td>
<td>${q.kpi_sub_total.toFixed(4)}</td>
    <td>${q.answer_notes || "-"}</td>
    <td>${q.answer_recommendations || "-"}</td>
                </tr>
            `;
        }
    
        html += `</tbody></table></div>`;
        return html;
    }

    function renderPercentageBar(percentage, level = "sub") {
        let color = "#be0000"; // Default: Weak (Red)
        let label = "Weak";
 
        if (percentage >= 50 && percentage <= 65) {
            color = "#ff0"; // Acceptable 
            label = "Acceptable";
        } else if (percentage >= 66 && percentage <= 75) {
            color = "#ffbe00"; // Good 
            label = "Good";
        } else if (percentage >= 76 && percentage <= 85) {
            color = "#b8fcb6"; // Very Good 
            label = "Very Good";
        } else if (percentage >= 86 && percentage <= 100) {
            color = "#11a342"; // Excellent (
            label = "Excellent";
        }
    
        const height = level === "main" ? "24px" : "18px";
    
        return `
            <div class="custom-progress-bar" style="height: ${height}; background-color: #e9ecef; border-radius: 6px; overflow: hidden; position: relative; margin-bottom: 5px;">
                <div style="
                    width: ${percentage}%;
                    background-color: ${color};
                    height: 100%;
                    transition: width 0.6s ease;
                "></div>
                <div style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    color: black;
                    font-size: 14px;
                ">${percentage}%</div>
            </div>
        `;
    }
    


    // function renderPercentageBar(percentage, level = "sub") {
    //     let color = "#28a745"; // green by default
    //     if (percentage < 50) color = "#dc3545"; // red
    //     else if (percentage < 75) color = "#ffc107"; // yellow
    
    //     const height = level === "main" ? "24px" : "18px";
    
    //     return `
    //         <div class="custom-progress-bar" style="height: ${height}; background-color: #e9ecef; border-radius: 6px; overflow: hidden; position: relative; margin-bottom: 5px;">
    //             <div style="
    //                 width: ${percentage}%;
    //                 background-color: ${color};
    //                 height: 100%;
    //                 transition: width 0.6s ease;
    //             "></div>
    //             <div style="
    //                 position: absolute;
    //                 top: 0;
    //                 left: 0;
    //                 right: 0;
    //                 height: 100%;
    //                 display: flex;
    //                 align-items: center;
    //                 justify-content: center;
    //                 font-weight: bold;
    //                 color: black;
    //                 font-size: 14px;
    //             ">${percentage}%</div>
    //         </div>
    //     `;
    // }
    


const  COL_N  = 6;


    function exportToExcel(reportData) {
        const wb = XLSX.utils.book_new();
        const ws_data = [];
        
        const now = new Date();
        const exportDate = now.toLocaleString();
        ws_data.push([`Exported on: ${exportDate}`]);
        ws_data.push([""]);
        
        const ws = XLSX.utils.aoa_to_sheet(ws_data);
        let row = 3;
        
        for (const [mainSection, mainData] of Object.entries(reportData)) {
            // Main Section Header (merged across columns and centered)
            const mainHeaderCell = `A${row}`;
            XLSX.utils.sheet_add_aoa(ws, [[`${mainSection}`]], { origin: mainHeaderCell });
            ws[mainHeaderCell].s = {

                fill: { fgColor: { rgb: "cfe2f3" } },
                font: { bold: true, sz: 14 },
                alignment: { horizontal: "center" }  // Center alignment
            };
            // Merge the main section header across all columns
            ws['!merges'] = ws['!merges'] || [];
            ws['!merges'].push({ s: { r: row - 1, c: 0 }, e: { r: row - 1, c: COL_N - 1  } });
            row++;
        
            for (const [subSection, subData] of Object.entries(mainData.sub_sections)) {
                // Sub Section Header (merged across columns and centered)
                const subHeaderCell = `A${row}`;
                XLSX.utils.sheet_add_aoa(ws, [[`  ${subSection}`]], { origin: subHeaderCell });
                ws[subHeaderCell].s = {
                    fill: { fgColor: { rgb: "ffe599" } },
                    font: { bold: true },
                    alignment: { horizontal: "center" }  // Center alignment
                };
                // Merge the sub-section header across all columns
                ws['!merges'].push({ s: { r: row - 1, c: 0 }, e: { r: row - 1, c: COL_N - 1  } });
                row++;
        
                const headers = [["    Question", "KPI Sub Total", "Answer %", "KPI", "Notes","Recommendations"]];
                XLSX.utils.sheet_add_aoa(ws, headers, { origin: `A${row}` });
        
                // Center-align the column headers
                for (let col = 0; col < COL_N; col++) {
                    const colLetter = String.fromCharCode(65 + col);
                    const cellRef = `${colLetter}${row}`;
                    ws[cellRef].s = {
                        fill: { fgColor: { rgb: "d9ead3" } },
                        font: { bold: true },
                        alignment: { horizontal: "center" }  // Center alignment
                    };
                }
                row++;
        
                subData.questions.forEach(q => {
                    XLSX.utils.sheet_add_aoa(ws, [[
                        `    ${q.question}`,
                        q.kpi_sub_total,
                        q.answer_percentage,
                        q.kpi,
                        q.answer_notes,
                        q.answer_recommendations,
                        
                    ]], { origin: `A${row}` });
                    row++;
                });
        
                // Sub Section Percentage with background color for entire row and centered text
                row++;
                const subPercentageRange = `A${row}:E${row}`;
                XLSX.utils.sheet_add_aoa(ws, [[
                    "    Sub Section Percentage:", "", "", "", "", `${subData.sub_percentage.toFixed(2)}%`
                ]], { origin: `A${row}` });
                for (let col = 0; col < COL_N; col++) {
                    const colLetter = String.fromCharCode(65 + col);
                    const cellRef = `${colLetter}${row}`;
                    ws[cellRef].s = {
                        fill: { fgColor: { rgb: "ffe599" } },
                        font: { bold: true },
                        alignment: { horizontal: "center" }  // Center alignment
                    };
                }
                row += 2;
            }
        
            // Main Section Percentage with background color for entire row and centered text
            const mainPercentageRange = `A${row}:E${row}`;
            XLSX.utils.sheet_add_aoa(ws, [[
                "Main Section Percentage:", "", "", "", "", `${mainData.main_percentage.toFixed(2)}%`
            ]], { origin: `A${row}` });
            for (let col = 0; col < COL_N; col++) {
                const colLetter = String.fromCharCode(65 + col);
                const cellRef = `${colLetter}${row}`;
                ws[cellRef].s = {
                    fill: { fgColor: { rgb: "cfe2f3" } },
                    font: { bold: true },
                    alignment: { horizontal: "center" }  // Center alignment
                };
            }
            row += 2;
        }
        
        // Apply some column widths for clarity
        ws['!cols'] = [
            { wch: 40 }, { wch: 20 }, { wch: 15 }, { wch: 20 }, { wch: 30 }
        ];
        
        XLSX.utils.book_append_sheet(wb, ws, "Survey Report");
        XLSX.writeFile(wb, "Styled_Survey_Report.xlsx");
    }
    
    



    
//  old  js lip no style

    // function exportToExcel(reportData) {
    //     const wb = XLSX.utils.book_new();
    //     const ws_data = [];
    
    //     for (const [mainSection, mainData] of Object.entries(reportData)) {
    //         ws_data.push([`${mainSection}`]);  // Main section as header
    
    //         for (const [subSection, subData] of Object.entries(mainData.sub_sections)) {
    //             ws_data.push([`  ${subSection}`]);
    //             ws_data.push(["    Question", "KPI Sub Total", "Answer %", "KPI", "Notes"]);
    
    //             subData.questions.forEach(q => {
    //                 ws_data.push([
    //                     `    ${q.question}`,
    //                     q.kpi_sub_total,
    //                     q.answer_percentage,
    //                     q.kpi,
    //                     q.answer_notes
    //                 ]);
    //             });
    
    //             // Sub-section percentage
    //             ws_data.push(["", "", "", "", ""]);
    //             ws_data.push([
    //                 "    Sub Section Percentage:",
    //                 "",
    //                 "",
    //                 "",
    //                 `${subData.sub_percentage.toFixed(2)}%`
    //             ]);
    //             ws_data.push([""]); // Empty row
    //         }
    
    //         // Main section percentage
    //         ws_data.push([""]);
    //         ws_data.push([
    //             "Main Section Percentage:",
    //             "",
    //             "",
    //             "",
    //             `${mainData.main_percentage.toFixed(2)}%`
    //         ]);
    //         ws_data.push([""]); // More spacing
    //     }
    
    //     const ws = XLSX.utils.aoa_to_sheet(ws_data);
    //     XLSX.utils.book_append_sheet(wb, ws, "Survey Report");
    
    //     XLSX.writeFile(wb, "Survey_Report.xlsx");
    // }
    

    
});