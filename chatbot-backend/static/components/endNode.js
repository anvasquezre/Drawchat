const nodeName = "endNode";

const component = `
<div>
  <div class="title-box end"><i class="far fa-calendar-times"></i>End session</div>
  <div class="box">
    <p>End session</p>
    <textarea df-text></textarea>
  </div>
</div>
`;

const menuIcon = `<div
class="drag-drawflow"
draggable="true"
ondragstart="drag(event)"
data-node="${nodeName}">
<i class="far fa-calendar-times"></i><span> End Node!</span>
<div id="description_end" style="display: none;">
    <p>End session</p>
</div>
</div>`
;

export const initEndNode = () => {
  const menu = document.getElementById("menu-container");
  menu.insertAdjacentHTML("beforeend", menuIcon);
  // Add event listener to show description when dropdown button is clicked
  var descriptionDiv = document.getElementById("description_end");

    // Get a reference to the element you want to click on
    var element = document.querySelector(`div.drag-drawflow[data-node=${nodeName}]`);

    // Add a click event listener to the element
    element.addEventListener("click", function () {
        // Toggle the display of the description div
        if (descriptionDiv.style.display === "none") {
            descriptionDiv.style.display = "block";
        } else {
            descriptionDiv.style.display = "none";
        }
    });
};

export const addEndNode = (editor, pos_x, pos_y) => {
  editor.addNode(
    nodeName,
    1,
    1,
    pos_x,
    pos_y,
    nodeName,
    { text: "" },
    component
  );
};
