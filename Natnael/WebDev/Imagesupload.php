 <?php
        $host ="localhost";
        $uname = "root";
        $pwd = '123456';
        $db_name = "master";

        $file_path = 'photo/';
        $result = mysqli_connect($host,$uname,$pwd) or die("Could not connect to database." .mysqli_error());
        mysqli_select_db($result,$db_name) or die("Could not select the databse." .mysqli_error());
        $image_query = mysqli_query($result,"select img_name,img_path from image_table");
        while($rows = mysqli_fetch_array($image_query))
        {
            $img_name = $rows['img_name'];
            $img_src = $rows['img_path'];
        ?>

        <div class="img-block">
        <img src="<?php echo $img_src; ?>" alt="" title="<?php echo $img_name; ?>" width="300" height="200" class="img-responsive" />
        <p><strong><?php echo $img_name; ?></strong></p>
        </div>

        <?php